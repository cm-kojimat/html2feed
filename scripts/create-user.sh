#!/usr/bin/env bash
set -xueo pipefail

while [[ $# -gt 0 ]]; do
  case $1 in
  --user-pool-id)
    user_pool_id=$2
    shift 2
    ;;
  --client-id)
    client_id=$2
    shift 2
    ;;
  --username)
    username=$2
    shift 2
    ;;
  --password)
    password=$2
    shift 2
    ;;
  *)
    echo "[ERROR] invalid arguments: $*" >&2
    exit 1
    ;;
  esac
done

aws cognito-idp admin-create-user \
  --user-pool-id "${user_pool_id}" \
  --username "${username}" || true
aws cognito-idp admin-set-user-password \
  --user-pool-id "${user_pool_id}" \
  --username "${username}" \
  --password "${password}" \
  --permanent
aws cognito-idp admin-initiate-auth \
  --user-pool-id "${user_pool_id}" \
  --client-id "${client_id}" \
  --auth-flow ADMIN_USER_PASSWORD_AUTH \
  --auth-parameters "USERNAME=${username},PASSWORD=${password}" \
  | jq -rc .AuthenticationResult.AccessToken
