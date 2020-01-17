set nocompatible              " required
filetype plugin on 

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
" add all your plugins here (note older versions of Vundle
" " used Bundle instead of Plugin)

Plugin 'gmarik/Vundle.vim'
Plugin 'Valloric/YouCompleteMe'
Plugin 'scrooloose/nerdtree'
Plugin 'jistr/vim-nerdtree-tabs'
Plugin 'SirVer/ultisnips'
Plugin 'honza/vim-snippets'
Plugin 'fatih/vim-go'
Plugin 'jiangmiao/auto-pairs'
Plugin 'tmhedberg/SimpylFold'
Plugin 'benmills/vimux'
Plugin 'tpope/vim-fugitive'
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
Plugin 'morhetz/gruvbox'

" All of your Plugins must be added before the following line
call vundle#end()            " required

syntax on
set noswapfile
set encoding=utf-8
set fileencoding=utf-8
set nu

colorscheme gruvbox
set background=dark
let g:gruvbox_contrast='hard'
let g:gruvbox_contrast_dark='hard'

set splitright
set splitbelow

" Close auto-complete window after use
let g:ycm_autoclose_preview_window_after_completion=1
let g:ycm_collect_identifiers_from_tags_files=1

" Nerdtree setup
map <C-o> :NERDTreeToggle<CR>
" Hide .pyc files from file tree
let NERDTreeIgnore=['\.pyc$', '\~$'] "ignore files in NERDTree

" Trigger configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
let g:UltiSnipsExpandTrigger="<C-q>"

if !exists('g:airline_symbols')
	let g:airline_symbols = {}
endif

" vim-airline setup
let g:airline_theme = 'dark_minimal'

let g:airline_powerline_fonts = 1
" unicode symbols
let g:airline_left_sep = '»'
let g:airline_left_sep = '▶'
let g:airline_right_sep = '«'
let g:airline_right_sep = '◀'
let g:airline_symbols.linenr = '␊'
let g:airline_symbols.linenr = '␤'
let g:airline_symbols.linenr = '¶'
let g:airline_symbols.branch = '⎇'
let g:airline_symbols.paste = 'ρ'
let g:airline_symbols.paste = 'Þ'
let g:airline_symbols.paste = '∥'
let g:airline_symbols.whitespace = 'Ξ'

" airline symbols
let g:airline_left_sep = ''
let g:airline_left_alt_sep = ''
let g:airline_right_sep = ''
let g:airline_right_alt_sep = ''
let g:airline_symbols.branch = ''
let g:airline_symbols.readonly = ''
let g:airline_symbols.linenr = ''
