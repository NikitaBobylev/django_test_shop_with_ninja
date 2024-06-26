DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
APP_FILE = docker_compose/app.yaml
MONITORING_FILE = docker_compose/monitoring.yaml
EXEC = docker exec -it
DB_CONTAINER = example-db
APP_CONTAINER = main-app
MONITORING_CONTAINER = apm-server
LOGS = docker logs
PYTHON_MANEGE = python manage.py
ENV_FILE = --env-file .env


.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up -d


.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f


.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down






.PHONY: app
app:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV_FILE} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f


.PHONY: app-down
app-down:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} down

.PHONY: restart
restart:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} down && ${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV_FILE} up --build -d



.PHONY: monitoring
monitoring:
	${DC} -f ${MONITORING_FILE} ${ENV_FILE} up --build -d

.PHONY: monitoring-logs
monitoring-logs:
	${DC} -f ${MONITORING_FILE} ${ENV_FILE} logs -f


.PHONY: monitoring-down
monitoring-down:
	${DC} -f ${MONITORING_FILE} down






.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} ${PYTHON_MANEGE} makemigrations


.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} ${PYTHON_MANEGE} migrate


.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER} ${PYTHON_MANEGE} createsuperuser

.PHONY: createapp
createapp:
	${EXEC} ${APP_CONTAINER} ${PYTHON_MANEGE} createapp

.PHONY: collectstatic
collectstatic:
	${EXEC} ${APP_CONTAINER} ${PYTHON_MANEGE} collectstatic

.PHONY: run-test
run-test:
	${EXEC} ${APP_CONTAINER} pytest