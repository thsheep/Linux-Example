K8S 踩坑指南

kube-apiserver报错： Unable to find suitable network address.error='Unable to select an IP.' . Try to set the AdvertiseAddress directly or provide a valid BindAddress to fix this

解决办法： 是默认网关没有配置的问题，比如默认网关是192.168.0.1 在命令行上添加默认网关:route add default gw  192.168.0.1确认网关已经配置好后，再一次启动apiserver（可以使用route -n查看默认网关是否已经配置好了）


## 故障排除记录：

1、首先确定问题是处在 pods 、Replication Controller 或者是 Service ？

2、调试一个Pod的第一步是看看它。使用以下命令检查Pod的当前状态和最近的事件：
	
	$ kubectl describe pods ${POD_NAME}

	看看pod中的容器的状态。他们都运行吗？有没有最近重启？ 根据pod的状态继续调试

	2.1 pod状态是pending

		如果一个Pod状态是Pending，这意味着它不能被调度到一个节点上。通常这是因为有一种类型的资源不足以防止调度，查看上面的kubectl describe ...命令的输出，
		应该有调度程序的消息，为什么它不能安排你的pod。理由包括：

			2.1.1 您没有足够的资源：
				
				您可能已经耗尽了集群中的CPU或内存供应，在这种情况下，您需要删除Pods，调整资源请求或将新节点添加到集群中。有关详细信息，请参阅Compute Resources文档。https://k8smeetup.github.io/docs/user-guide/compute-resources/#my-pods-are-pending-with-event-message-failedscheduling

			2.1.2 你正在使用hostPort：

				当您将Pod绑定到hostPort时，可以安排pod的数量有限的位置。在大多数情况下，hostPort是不必要的，尝试使用Service对象来显示您的Pod。如果您需要hostPort，那么您只能安排与Kubernetes群集中的节点一样多的Pods

	2.2 pod状态是waiting：

		如果一个Pod卡在等待状态，那么它已被调度到一个工作节点，但是它不能在该机器上运行。再次查看kubectl describe... pod waiting最常见原因是无法拉取镜像。有三件事要检查：

			确保你的镜像名字正确

			存储库是否有该镜像

			手动运行docker pull <images> 看看是否能获取成功

	2.3 pod 状态是crashing 或者 otherwise unhealthy

		首先，查看当前容器的日志：
			$ kubectl logs ${POD_NAME} ${CONTAINER_NAME}

		如果您的容器先前已崩溃，则可以使用以下命令访问上一个容器的崩溃日志：

			$ kubectl logs --previous ${POD_NAME} ${CONTAINER_NAME}

		或者，您可以使用exec在该容器内运行命令：

			$ kubectl exec ${POD_NAME} -c ${CONTAINER_NAME} -- ${CMD} ${ARG1} ${ARG2} ... ${ARGN}

		请注意，-c $ {CONTAINER_NAME}是可选的，对于仅包含单个容器的Pods，可以省略。 例如，要查看正在运行的Cassandra pod的日志，可以运行它：

			$ kubectl exec cassandra -- cat /var/log/cassandra/system.log

		如果这些方法都不起作用，您可以找到运行该pod的主机并使用SSH连接到该主机，处理问题。并在github发布issue详细描述你的问题。 

	2.4 pod 处于运行状态但是并没有按照我预期的方式运行。

		如果您的pod不符合您的预期，则可能是您的pod描述中出现错误（例如本地计算机上的mypod.yaml文件），并且在创建pod时默认忽略该错误，通常情况下，pod描述的一部分不正确地嵌套，或键入的名称不正确，因此该键被忽略。

		首先要做的是删除您的pod，并尝试使用--validate选项重新创建它。

		接下来要检查的是，apiserver上的pod是否与您要创建的pod相匹配（例如，在本地机器上的yaml文件中）例如运行：

			kubectl get pods/mypod -o yaml > mypod-on-apiserver.yaml

		然后手动对比原始pod的描述，与返回的是否相同。


3、Replication Controllers 处理

	Replication Controllers相当简单。他们可以创建Pods或者不能。如果无法创建pod，请参阅上述说明来调试您的pod（说白了 这玩意儿就是管复制的）

		可使用 kubectl describe rc ${CONTROLLER_NAME} 来获取相关信息


4、 Services 调试

	Services提供一组pod的负载平衡，有几个常见的问题可能会导致Services无法正常工作。以下说明将有助于调试Services问题。

	首先，验证服务是否有端点。对于每个Service对象，apiserver使端点资源可用。
	您可以查看此资源：

		$ kubectl get endpoints ${SERVICE_NAME}

	确保端点与您期望成为Service成员的容器数匹配 例如你有一个服务 标签是：
		...
		spec:
		  - selector:
		     name: nginx
		     type: frontend

	你可以使用：

		$ kubectl get pods --selector=name=nginx,type=frontend

	列出与此选择器匹配的pod，验证列表是否符合您期望提供Services的Pods。
	如果pod的列表符合预期，但是您的端点仍然为空，那么您可能没有暴露出正确的端口.如果您的服务指定了一个containerPort，但是所选的Pods没有列出该端口，则不会将其添加到端点列表.验证pod的containerPort是否与Service的containerPort匹配


5、网络流量不转发
	
	如果您可以连接到服务，但连接立即丢弃，并且端点列表中有端点，代理可能无法与您的pods联系。

	有三件事要检查：

		你的Pod是否正常工作，重启启动并调试Pod

		你可以直接连接到你的pod吗？获取Pod的IP地址，并尝试直接连接到该IP。

		您的应用程序是否在您配置的端口上服务？Kubernetes不进行端口重映射，因此如果您的应用程序在8080服务，则containerPort字段需要为8080