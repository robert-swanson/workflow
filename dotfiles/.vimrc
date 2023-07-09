" Escape Character
inoremap ;; <Esc>
noremap ;; :qa<Enter>
noremap w;; :wqa<Enter>

" Line Nuumbers
 set number relativenumber

" Indentation
set expandtab ts=4 sw=4 ai

" Syntax Highlighting
filetype plugin indent on
syntax on
set hlsearch

set foldmethod=syntax

colorscheme gruvbox
set background=dark

" Window keybindings
noremap <C-h> <C-w>h
noremap <C-j> <C-w>j
noremap <C-k> <C-w>k
noremap <C-l> <C-w>l
set splitright

" Tab keybindings
map <S-h> :tabp<cr>
map <S-l> :tabn<cr>

" File buffer movement
map <S-k> :bn<cr>
map <S-j> :bp<cr>

" Zoom / Restore window.
function! s:ZoomToggle() abort
    if exists('t:zoomed') && t:zoomed
        execute t:zoom_winrestcmd
        let t:zoomed = 0
    else
        let t:zoom_winrestcmd = winrestcmd()
        resize
        vertical resize
        let t:zoomed = 1
    endif
endfunction
command! ZoomToggle call s:ZoomToggle()
nnoremap <silent> <S-z> :ZoomToggle<CR>

nnoremap ,<space> :nohlsearch<CR>
