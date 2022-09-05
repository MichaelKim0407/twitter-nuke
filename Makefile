build:
	docker-compose build --pull

pip_lock:
	docker-compose -f docker-compose.pip-lock.yml run --rm pip_lock
