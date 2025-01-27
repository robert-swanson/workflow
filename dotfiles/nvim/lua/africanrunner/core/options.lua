local opt = vim.opt
local api = vim.api

opt.relativenumber = true
opt.number = true

opt.tabstop = 4
opt.shiftwidth = 4
opt.expandtab = true
opt.autoindent = true

opt.ignorecase = true
opt.smartcase = true
opt.hlsearch = true
opt.incsearch = true

opt.termguicolors = true
opt.background = 'dark'

opt.splitright = true
opt.splitbelow = true

-- opt.endofline = false

-- opt.iskeyword:append('-')

opt.clipboard = 'unnamed'
-- opt.mouse = ''

-- To-do: Format nicely, add git buffers
api.nvim_create_autocmd({ 'BufEnter', 'BufWinEnter' }, {
  pattern = { '*.md', '*.txt', '*.json', '*.jsonnet' },
  callback = function()
    opt.tabstop = 2
    opt.shiftwidth = 2
    opt.spell = true
    opt.linebreak = true
    opt.signcolumn = 'no'
  end,
})

api.nvim_create_autocmd({ 'BufEnter', 'BufWinEnter' }, {
  pattern = { '*.lua', '*.js', '*.ts' },
  callback = function()
    opt.tabstop = 2
    opt.shiftwidth = 2
  end,
})

-- https://github.com/google/vim-jsonnet/issues/18
api.nvim_create_autocmd({ 'BufRead', 'BufNewFile' }, {
  pattern = { '*.libsonnet' },
  callback = function()
    opt.filetype = 'jsonnet'
  end,
})

-- set colorscheme to nightfly with protected call
-- in case it isn't installed
local status, _ = pcall(vim.cmd, 'colorscheme nightfly')
if not status then
  print('Colorscheme not found!') -- print error if colorscheme not installed
  return
end
