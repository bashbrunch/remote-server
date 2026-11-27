URL="http://localhost:8000"
SID="test-session-id"
tmp=$(mktemp -d)

printf "" >> "${tmp}/failed"
printf "" >> "${tmp}/passed"

expect() {
  local method=$1
  local endpoint=$2
  local password=$3
  local content=$4
  local expected=$5

  local response=$(curl -s "${URL}/${SID}${endpoint}" \
    -X "${method}" \
    -H "Authorization: ${password}" \
    -d "${content}" \
    -w "\n%{http_code}\n%{time_total}"
  )

  local result=$(echo "${response}" | tail -r | tail -n +3 | tail -r)
  local status=$(echo "${response}" | tail -n 2 | head -n 1)
  local latency=$(echo "${response}" | tail -n 1)

  if grep -qzE "${expected}" <<< "${result}"; then
    printf "passed ${status} ${latency}\n" >> "${tmp}/passed"
    return 0
  fi

  printf "Test failed:\n"
  printf "  Endpoint: [${method}] ${endpoint}\n"
  printf "  Password: '${password}'\n"
  printf "  Content: '${content}'\n"
  printf "  Expected: '${expected}'\n"
  printf "  Received: '${result}'\n"

  printf "failed\n" >> "${tmp}/failed"
}

check() {
  local idem=$1
  local label=$2
  local index=$3

  if [[ -z "$index" ]]; then
    index=1
  fi

  result=$(curl -s "${URL}/${SID}_${idem}/${label}")
  printf "$result" | head -n $((index)) | tail -n 1
}

