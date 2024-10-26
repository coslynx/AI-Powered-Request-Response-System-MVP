#!/bin/bash
set -euo pipefail

# Environment setup
PROJECT_ROOT=$(dirname "$0")
LOG_FILE="$PROJECT_ROOT/logs/startup.log"
PID_FILE="$PROJECT_ROOT/logs/startup.pid"
DATABASE_TIMEOUT=30
HEALTHCHECK_INTERVAL=5

# Function definitions
log_info() {
  echo "$(date +"%Y-%m-%d %H:%M:%S") [INFO] $*" >> "$LOG_FILE"
}

log_error() {
  echo "$(date +"%Y-%m-%d %H:%M:%S") [ERROR] $*" >&2
}

cleanup() {
  log_info "Cleaning up process..."
  if [ -f "$PID_FILE" ]; then
    kill -9 $(cat "$PID_FILE") 2>/dev/null
    rm "$PID_FILE"
  fi
}

check_dependencies() {
  log_info "Checking dependencies..."
  command -v docker >/dev/null 2>&1 || {
    log_error "Docker is required. Please install Docker."
    exit 1
  }
  command -v docker-compose >/dev/null 2>&1 || {
    log_error "Docker Compose is required. Please install Docker Compose."
    exit 1
  }
}

check_port() {
  local port="$1"
  nc -z localhost "$port" >/dev/null 2>&1 && return 0 || return 1
}

wait_for_service() {
  local service="$1"
  local port="$2"
  local timeout="$3"
  local counter=0

  log_info "Waiting for $service to start on port $port..."
  while [ "$counter" -lt "$timeout" ]; do
    if check_port "$port"; then
      log_info "$service is running."
      return 0
    fi
    sleep "$HEALTHCHECK_INTERVAL"
    counter=$((counter + 1))
  done
  log_error "$service failed to start on port $port."
  exit 1
}

verify_service() {
  local service="$1"
  local port="$2"
  local timeout="$3"

  log_info "Verifying $service on port $port..."
  wait_for_service "$service" "$port" "$timeout"
  log_info "$service is healthy."
}

start_database() {
  log_info "Starting PostgreSQL database..."
  docker-compose up -d database
  wait_for_service "PostgreSQL" 5432 "$DATABASE_TIMEOUT"
}

start_backend() {
  log_info "Starting backend server..."
  docker-compose up -d backend
  wait_for_service "Backend" 8000 "$DATABASE_TIMEOUT"
}

store_pid() {
  local pid="$1"
  local file="$2"
  echo "$pid" > "$file"
}

# Main script execution
trap cleanup EXIT ERR

check_dependencies
source "$PROJECT_ROOT/.env"
log_info "Environment variables loaded."

start_database
start_backend

log_info "Services started successfully."