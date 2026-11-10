TESTS=$(dirname "$0")
source "$TESTS/setup.sh"

expect "POST" "_1/sessions" "" "" "ok"
expect "POST" "_2/sessions" "" "pwd" "ok"
expect "POST" "_2/sessions" "" "pwd" "access denied"
expect "POST" "_2/sessions" "pwd" "password" "ok"

expect "DELETE" "_1/sessions" "" "" "ok"
expect "DELETE" "_1/sessions" "" "" "access denied"
expect "DELETE" "_2/sessions" "pwd" "" "access denied"
expect "DELETE" "_2/sessions" "password" "" "ok"

expect "GET" "/sessions" "" "" "access denied"
expect "POST" "/sessions" "" "" "ok"
expect "GET" "/sessions" "" "" "ok"

expect "POST" "/messages" "" "hi 1" "ok"
expect "POST" "/messages" "" "hi 2" "ok"
expect "POST" "/messages" "" "hi 3" "ok"

expect "GET" "/messages" "" "" "[^\n]*\nhi 1"
expect "GET" "/messages" "" "" "[^\n]*\nhi 1"

key=$(curl -s "${URL}/${SID}/messages" | head -n 1)

expect "DELETE" "/messages/${key}" "" "" "ok"
expect "DELETE" "/messages/${key}" "" "" "key mismatch"

expect "GET" "/messages" "" "" "[^\n]*\nhi 2"

expect "DELETE" "/sessions" "" "" "ok"

