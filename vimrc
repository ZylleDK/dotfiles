set nocompatible              " required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
" add all your plugins here (note older versions of Vundle
" " used Bundle instead of Plugin)

Plugin 'gmarik/Vundle.vim'
Plugin 'tmhedberg/SimpylFold'
Plugin 'Valloric/YouCompleteMe'
Plugin 'scrooloose/nerdtree'
Plugin 'jistr/vim-nerdtree-tabs'
Plugin 'SirVer/ultisnips'
Plugin 'honza/vim-snippets'
Plugin 'fatih/vim-go'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

set noswapfile
set encoding=utf-8
set nu

set background=dark
hi Comment ctermfg=LightGreen

" Setup split window order
set splitbelow
set splitright

" Split navigations:
"<CTRL>+J --> Move to the split below
"<CTRL>+K --> Move to the split above
"<CTRL>+L --> Move to the split to the right
"<CTRL>+H --> Move to the split to the left
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" Enable code folding
set foldmethod=indent
set foldlevel=0
" Fold and unfold using the space-bar
nnoremap <space> za
let g:SimplyFold_docstring_preview=1

" Close auto-complete window after use
let g:ycm_autoclose_preview_window_after_completion=1
let g:ycm_collect_identifiers_from_tags_files=1


" Nerdtree setup
map <C-t> :NERDTreeToggle<CR>
" Hide .pyc files from file tree
let NERDTreeIgnore=['\.pyc$', '\~$'] "ignore files in NERDTree

" Trigger configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
let g:UltiSnipsExpandTrigger="<C-q>"
