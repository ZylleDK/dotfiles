"Set up tab-indentation
filetype plugin indent on
" show existing tab with 4 spaces width
set tabstop=4
" when indenting with '>', use 4 spaces width
set shiftwidth=4
" On pressing tab, insert 4 spaces
set expandtab

" Enable folding
set foldmethod=indent
set foldlevel=0

" fold and un-fold code using spacebar
nnoremap <special><space> za

let g:SimplyFold_docstring_preview=1
