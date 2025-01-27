local ensure_packer = function()
  local fn = vim.fn
  local install_path = fn.stdpath('data') .. '/site/pack/packer/start/packer.nvim'
  if fn.empty(fn.glob(install_path)) > 0 then
    fn.system({ 'git', 'clone', '--depth', '1', 'https://github.com/wbthomason/packer.nvim', install_path })
    vim.cmd([[packadd packer.nvim]])
    return true
  end
  return false
end
local packer_bootstrap = ensure_packer()

vim.cmd([[ 
  augroup packer_user_config
    autocmd!
    autocmd BufWritePost packer.lua source <afile> | PackerSync
  augroup end
]])

local status, packer = pcall(require, 'packer')
if not status then
  return
end

return packer.startup(function(use)
  use('wbthomason/packer.nvim')
  use('bluz71/vim-nightfly-guicolors')

  use('nvim-lua/plenary.nvim')

  use('christoomey/vim-tmux-navigator')

  use('numToStr/Comment.nvim')

  use({ 'nvim-telescope/telescope-fzf-native.nvim', run = 'make' })
  use({ 'nvim-telescope/telescope.nvim', branch = '0.1.x' })

  use('ThePrimeagen/harpoon')

  use('nvim-tree/nvim-tree.lua')
  use('kyazdani42/nvim-web-devicons')

  use('nvim-lualine/lualine.nvim')

  use('f-person/git-blame.nvim')

  use('neovim/nvim-lspconfig')
  use('hrsh7th/cmp-nvim-lsp')
  use('hrsh7th/cmp-buffer')
  use('hrsh7th/cmp-path')
  use('hrsh7th/cmp-cmdline')
  use('hrsh7th/nvim-cmp')

  use('L3MON4D3/LuaSnip')
  use('saadparwaiz1/cmp_luasnip')
  use('rafamadriz/friendly-snippets')

  use('williamboman/mason.nvim')
  use('williamboman/mason-lspconfig.nvim')

  use('sindrets/diffview.nvim')

  -- To-do: ts plugins

  use({ 'glepnir/lspsaga.nvim', branch = 'main', commit = 'b7b4777369b441341b2dcd45c738ea4167c11c9e' }) -- enhanced lsp uis
  use('onsails/lspkind.nvim') -- vs-code like icons for autocompletion

  use('jose-elias-alvarez/null-ls.nvim') -- configure formatters & linters
  use('jayp0521/mason-null-ls.nvim') -- bridges gap b/w mason & null-ls

  use({
    'nvim-treesitter/nvim-treesitter',
    run = function()
      local ts_update = require('nvim-treesitter.install').update({ with_sync = true })
      ts_update()
    end,
  })

  use('windwp/nvim-autopairs') -- autoclose parens, brackets, quotes, etc...
  use({ 'windwp/nvim-ts-autotag', after = 'nvim-treesitter' }) -- autoclose tags

  use('lewis6991/gitsigns.nvim')

  use('ojroques/nvim-osc52')

  if packer_bootstrap then
    require('packer').sync()
  end
end)
