local lspconfig_setup, lspconfig = pcall(require, "lspconfig")
if not lspconfig_setup then
  return
end

lspconfig.rust_analyzer.setuip()

local on_attach = function(client, bufnr)
  local bufopts = { noremap = true, silent = true, buffer = bufnr }
  local keymap = vim.keymap
  keymap.set("n", "gD", vim.lsp.buf.declaration, bufopts)
  keymap.set("n", "gd", vim.lsp.buf.definition, bufopts)
  keymap.set("n", "K", vim.lsp.buf.hover, bufopts)
end
