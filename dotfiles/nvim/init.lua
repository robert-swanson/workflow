require('africanrunner')

-- local capabilities = vim.lsp.protocol.make_client_capabilities()
-- capabilities.offsetEncoding = { "utf-16" }
-- require("lspconfig").clangd.setup({ capabilities = capabilities })

-- To-do: Cite sources

vim.lsp.set_log_level('off')

vim.cmd('set runtimepath^=~/.vim runtimepath+=~/.vim/after') 
vim.o.packpath = vim.o.runtimepath vim.cmd('source ~/.vimrc')
