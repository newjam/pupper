if 10 > flag then true else false

let target = 38 in
let search = fn (i : int ) => fn (j : int ) =>
  if i = j 
  then i
  else 
    let k = (i + j) /2 in
    if target > k 
    then search k j
    else search i k
in search 0 100

