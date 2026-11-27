expect_queue() {
  local idem=$1
  local label=$2

  expect "POST" "_${idem}/${label}" "" "value 1" "ok"
  expect "POST" "_${idem}/${label}" "" "value 2" "ok"
  expect "POST" "_${idem}/${label}" "" "value 3" "ok"

  expect "GET" "_${idem}/${label}" "" "" "[^\n]*\nvalue 1"
  expect "GET" "_${idem}/${label}" "" "" "[^\n]*\nvalue 1"

  expect "GET" "_${idem}/${label}/stream" "" "" "value 1\nvalue 2\nvalue 3"
  expect "GET" "_${idem}/${label}/keys" "" "" "^[a-f|0-9]*\n[a-f|0-9]*\n[a-f|0-9]*\n$"

  key1=$(check "${idem}" "${label}/keys" 1)
  key2=$(check "${idem}" "${label}/keys" 2)

  expect "GET" "_${idem}/${label}/${key1}" "" "" "value 1"
  expect "GET" "_${idem}/${label}/${key2}" "" "" "value 2"

  expect "DELETE" "_${idem}/${label}/${key1}" "" "" "ok"
  expect "DELETE" "_${idem}/${label}/${key1}" "" "" "key mismatch"

  expect "GET" "_${idem}/${label}/$key1" "" "" "key mismatch"

  expect "GET" "_${idem}/${label}" "" "" "[^\n]*\nvalue 2"
}

