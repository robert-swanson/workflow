local setup, nvimtree = pcall(require, 'nvim-tree')
if not setup then
  return
end

vim.g.loaded = 1
vim.g.loaded_netrwPlugin = 1

local keymap = vim.keymap

keymap.set('n', '<leader>e', ':NvimTreeToggle<CR>')

nvimtree.setup({
  update_focused_file = {
    enable = true,
    update_root = true,
  },
  view = {
    width = 75,
    relativenumber = true,
  },
  actions = {
    open_file = {
      quit_on_open = true,
    },
  },
})
