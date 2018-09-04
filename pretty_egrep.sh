reset && ls -t | grep -E ".out$" | head -n 1 | xargs -I{} tail -f -n +0 {} | nl | grep -v -E "getDataset()|getQuest()" | grep -E "$1" | cut -c 1-1024 | xargs -d '\n' -I{} printf "{}\n\n"
