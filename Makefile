
DOCKERHUB_USERNAME:=poridhi
tag:=v1.1

fe:
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-frontend:${ftag} ./frontend
	@ docker push $(DOCKERHUB_USERNAME)/todo-frontend:${ftag}


build:
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-frontend:${ftag} ./frontend
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-backend:${tag} ./backend
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-postgres:${tag} ./database

docker-push:
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-frontend:${ftag} ./frontend
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-backend:${tag} ./backend
	@ docker build -t $(DOCKERHUB_USERNAME)/todo-postgres:${tag} ./database
	@ docker push $(DOCKERHUB_USERNAME)/todo-frontend:${ftag}
	@ docker push $(DOCKERHUB_USERNAME)/todo-backend:${tag}
	@ docker push $(DOCKERHUB_USERNAME)/todo-postgres:${tag}

deploy:
	@ kubectl apply -f k8s/

clean:
	@ kubectl delete -f k8s/

pods:
	@ kubectl get pods

push:
	@ docker build -t $(DOCKERHUB_USERNAME)/my-backend:${tag} .
	@ docker push $(DOCKERHUB_USERNAME)/my-backend:${tag}

