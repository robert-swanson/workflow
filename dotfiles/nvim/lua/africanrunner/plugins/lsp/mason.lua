local mason_status, mason = pcall(require, 'mason')
if not mason_status then
  return
end

local mason_lspconfig_status, mason_lspconfig = pcall(require, 'mason-lspconfig')
if not mason_lspconfig_status then
  return
end

local mason_null_ls_status, mason_null_ls = pcall(require, 'mason-null-ls')
if not mason_null_ls_status then
  return
end

mason.setup()

mason_lspconfig.setup({
  ensure_installed = {
    'rust_analyzer',
    -- 'jdtls',
    'jedi_language_server',
    -- 'sumneko_lua',
    'lua_ls',
    'clangd',
    'jsonnet_ls',
    -- 'gopls',
  },
})

mason_null_ls.setup({
  ensure_installed = {
    'prettier', -- ts/js formatter
    'stylua', -- lua formatter
    'eslint_d', -- ts/js linter
    -- "autopep8", -- python formatter
    -- "black",
    'flake8', -- python linter
    'yapf', -- python formatter
    'mypy',
    'cpplint', -- python formatter
    'clang_format',
    'taplo',
  },
  automatic_installation = true,
})
