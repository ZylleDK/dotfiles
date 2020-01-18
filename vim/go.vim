set nocompatible
set nobackup
set nowritebackup
set noswapfile

filetype plugin on

set mouse=a

" To get hover working in the terminal we need to set ttymouse. See
"
" :help ttymouse
"
" for the appropriate setting for your terminal. Note that despite the
" automated tests using xterm as the terminal, a setting of ttymouse=xterm
" does not work correctly beyond a certain column number (citation needed)
" hence we use ttymouse=sgr
set ttymouse=sgr

" Suggestion: By default, govim populates the quickfix window with diagnostics
" reported by gopls after a period of inactivity, the time period being
" defined by updatetime (help updatetime). Here we suggest a short updatetime
" time in order that govim/Vim are more responsive/IDE-like
set updatetime=500

" Suggestion: To make govim/Vim more responsive/IDE-like, we suggest a short
" balloondelay
set balloondelay=250

" Suggestion: Turn on the sign column so you can see error marks on lines
" where there are quickfix errors. Some users who already show line number
" might prefer to instead have the signs shown in the number column; in which
" case set signcolumn=number
set signcolumn=yes

" Suggestion: Turn on syntax highlighting for .go files. You might prefer to
" turn on syntax highlighting for all files, in which case
"
syntax on

" Suggestion: turn on auto-indenting. If you want closing parentheses, braces
" etc to be added, https://github.com/jiangmiao/auto-pairs. In future we might
" include this by default in govim.
set autoindent
set smartindent
filetype indent on

" Suggestion: define sensible backspace behaviour. See :help backspace for
" more details
set backspace=2

" Suggestion: show info for completion candidates in a popup menu
if has("patch-8.1.1904")
  set completeopt+=popup
  set completepopup=align:menu,border:off,highlight:Pmenu
endif

"Set up tab-indentation
filetype plugin indent on
" show existing tab with 4 spaces width
set tabstop=2
" when indenting with '>', use 4 spaces width
set shiftwidth=2
" On pressing tab, insert 4 spaces
set expandtab

let g:go_def_mode='gopls'
let g:go_info_mode='gopls'
let g:UltiUltiSnipsExpandTrigger="<C-j>"
map <special><F4> :GoFmt<CR>
imap <special><F4> <esc>:GoFmt<CR>
map <special><F5> :call VimuxRunCommandInDir("go run", 1)<CR>
imap <special><F5> <esc>:call VimuxRunCommandInDir("go run", 1)<CR>
map <special><F6> :call VimuxRunCommandInDir("go build", 1)<CR>
imap <special><F6> <esc>:call VimuxRunCommandInDir("go build", 1)<CR>
map <special><F12> :call VimuxRunCommandInDir("git merge ", 0)
imap <special><F12> <esc>:call VimuxRunCommandInDir("git merge ", 0)
nmap <special><Delete> :call VimuxCloseRunner()<CR>
