count() {
  local category=$1
  grep "${category}" "${tmp}/${category}" | wc -l | xargs
}

latency_p95() {
  local category=$1
  local val=$(sort -k3,3n "${tmp}/${category}" | awk '
    { a[NR]=$3 }
    END {
      if (NR > 0) print a[int(NR * 0.95 + 0.999)] * 1000
    }
  ')

  printf "%.3f ms\n" "${val:-0}"
}

latency_avg() {
  local category=$1
  local val=$(awk '
    { total += $3; count++ }
    END {
      if (count > 0) print total / count * 1000; else print 0
    }
  ' "${tmp}/${category}")

  printf "%.3f ms\n" "${val:-0}"
}

latency_max() {
  local category=$1
  local val=$(sort -k3,3n "${tmp}/${category}" | tail -n 1 | awk '{ print $3 * 1000 }')

  printf "%.3f ms\n" "${val:-0}"
}

show_analytics() {
  local passed=$(count "passed")
  local failed=$(count "failed")

  local p_lat_p95=$(latency_p95 "passed")
  local p_lat_avg=$(latency_avg "passed")
  local p_lat_max=$(latency_max "passed")

  local f_lat_p95=$(latency_p95 "failed")
  local f_lat_avg=$(latency_avg "failed")
  local f_lat_max=$(latency_max "failed")

  printf "Passed: ${passed}\n"
  printf "  - Avg: ${p_lat_avg}\n"
  printf "  - P95: ${p_lat_p95}\n"
  printf "  - Max: ${p_lat_max}\n"

  printf "\n"

  printf "Failed: ${failed}\n"
  printf "  - Avg: ${f_lat_avg}\n"
  printf "  - P95: ${f_lat_p95}\n"
  printf "  - Max: ${f_lat_max}\n"

  printf "\nTests completed.\n"

  if [[ ${failed} -eq 0 ]]; then
    printf "All tests passed!\n"
  else
    printf "Some tests failed.\n"
  fi
}

trap show_analytics EXIT

