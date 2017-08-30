





Post
(https://mail-index.netbsd.org/tech-userlevel/2012/12/02/msg006954.html)

regexp word boundaries
                \<      \b      [[:<:]]
awk             not     not     not
gawk            works   not     not
mawk            not     not     not
bsd grep        not     not     works
gnu grep        works   works   not
ed              not     not     works
emacs20         works   works   not
emacs22         works   works   not
less            not     not     works
nvi             works   not     works
perl            not     works   not
pcregrep        not     works   not
sed             not     not     works
freebsd vile    not     works   not
netbsd vile     works   not     not
vim             works   not     not
solaris awk     not     not     not  
solaris ed      works   not     not
solaris grep    not     not     not
solaris sed     works   not     not

Response
(https://mail-index.netbsd.org/tech-userlevel/2012/12/03/msg006955.html)
"without version numbers, I can only guess what you're referring to"
