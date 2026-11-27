idem=$RANDOM_$RANDOM

expect "GET" "../../" "" "" "Hello, Brunch OTN Server"
expect "GET" "../../health" "" "" "healthy"
expect "GET" "../../version" "" "" $(cat version)

expect "POST" "_${idem}_1/sessions" "" "" "ok"
expect "POST" "_${idem}_2/sessions" "" "pwd" "ok"
expect "POST" "_${idem}_2/sessions" "" "pwd" "access denied"
expect "POST" "_${idem}_2/sessions" "pwd" "password" "ok"

expect "DELETE" "_${idem}_1/sessions" "" "" "ok"
expect "DELETE" "_${idem}_1/sessions" "" "" "access denied"
expect "DELETE" "_${idem}_2/sessions" "pwd" "" "access denied"
expect "DELETE" "_${idem}_2/sessions" "password" "" "ok"

