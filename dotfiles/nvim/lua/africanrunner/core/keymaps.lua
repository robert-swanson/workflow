vim.g.mapleader = ' '

local keymap = vim.keymap

keymap.set('n', '<leader>h', ':noh<CR>')
keymap.set('n', '<leader>o', 'M<C-6>')

keymap.set('n', '<leader>p', ':bprev<CR>')
keymap.set('n', '<leader>n', ':bnext<CR>')

keymap.set('n', '<leader>c', ':set cursorcolumn!<CR>')

-- keymap.set('n', '<leader>h', function()
--   vim.lsp.buf.document_highlight()
-- end)

keymap.set('n', '<leader>jc', ':e %<.cc<CR>')
keymap.set('n', '<leader>jh', ':e %<.h<CR>')
keymap.set('n', '<leader>jt', ':e %<_test.cc<CR>')
