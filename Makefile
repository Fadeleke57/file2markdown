start:
	uvicorn main:app --reload --port 4000

docker-start:
	docker-compose up --build

docker-stop:
	docker-compose down