.PHONY: serve
serve:
	docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d db
	docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d flyway
	docker-compose -f docker-compose.yml -f docker-compose.local.yml up webserver
