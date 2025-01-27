vim.g.gitblame_enabled = 0
vim.g.gitblame_date_format = '%r'
vim.g.gitblame_message_template = '  <author>, <date> • <summary>'
-- vim.g.gitblame_highlight_group = 'Question'

vim.keymap.set('n', '<leader>g', ':GitBlameToggle<CR>')
