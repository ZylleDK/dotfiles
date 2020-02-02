filetype plugin indent on
set tabstop=2
set shiftwidth=2
set expandtab

map <special><F5> :call VimuxRunCommandInDir("pdflatex", 1)<CR>
imap <special><F5> <esc>:call VimuxRunCommandInDir("pdflatex", 1)<CR>
nmap <special><Delete> :call VimuxCloseRunner()<CR>
