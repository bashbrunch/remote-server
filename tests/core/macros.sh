expect_queue() {
  local idem=$1
  local label=$2

  expect "POST" "_${idem}/${label}" "" "value 1" "ok"
  expect "POST" "_${idem}/${label}" "" "value 2" "ok"
  expect "POST" "_${idem}/${label}" "" "value 3" "ok"

  expect "GET" "_${idem}/${label}" "" "" "[^\n]*\nvalue 1"
  expect "GET" "_${idem}/${label}" "" "" "[^\n]*\nvalue 1"

  key=$(curl -s "${URL}/${SID}_${idem}/${label}" | head -n 1)

  expect "DELETE" "_${idem}/${label}/${key}" "" "" "ok"
  expect "DELETE" "_${idem}/${label}/${key}" "" "" "key mismatch"

  expect "GET" "_${idem}/${label}" "" "" "[^\n]*\nvalue 2"
}

