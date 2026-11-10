URL="http://localhost:8000"
SID="test-session-id"

passed=0
failed=0

expect() {
  local method=$1
  local endpoint=$2
  local password=$3
  local content=$4
  local expected=$5

  local result=$(curl -s "${URL}/${SID}${endpoint}" \
    -X "${method}" \
    -H "Authorization: ${password}" \
    -d "${content}"
  )

  if ! grep -qzE "${expected}" <<< "${result}"; then
    printf "Test failed:\n"
    printf "  Endpoint: [${method}] ${endpoint}\n"
    printf "  Password: '${password}'\n"
    printf "  Content: '${content}'\n"
    printf "  Expected: '${expected}'\n"
    printf "  Received: '${result}'\n"

    failed=$((failed + 1))
  else
    passed=$((passed + 1))
  fi
}

post() {
  printf "Passed: ${passed}\n"
  printf "Failed: ${failed}\n"

  printf "\nTests completed.\n"

  if [[ ${failed} -eq 0 ]]; then
    printf "All tests passed!\n"
  else
    printf "Some tests failed.\n"
  fi
}

trap post EXIT

