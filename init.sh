#!/bin/bash
docker-compose down -v
docker-compose build
docker-compose up -d kong-db
docker-compose up -d keycloak-db
sleep 30
cat dump_kong.sql | docker kong-db psql -U postgres -d postgres
cat dump_keycloak.sql | docker exec -i keycloak-db psql -U postgres -d postgres
docker-compose up