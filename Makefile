start:
	uvicorn main:app --reload --port 8080

docker-start:
	docker-compose up --build

docker-stop:
	docker-compose down