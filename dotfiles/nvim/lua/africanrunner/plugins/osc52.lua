local setup, osc52 = pcall(require, 'osc52')
if not setup then
  return
end

osc52.setup()

vim.keymap.set('v', '<leader>c', osc52.copy_visual)

vim.keymap.set('n', '<leader>l', function()
  local origin_url = vim.fn.system('git config --get remote.origin.url')
  local project, repo = string.gmatch(origin_url, '(%w+)/(%w+).git')()

  local absolute_repo_root = vim.fn.system('git rev-parse --show-toplevel')
  local absolute_file_path = vim.fn.system('pwd') .. '/' .. vim.fn.expand('%')
  local local_file_path = string.sub(absolute_file_path, string.len(absolute_repo_root))

  osc52.copy('https://stash/projects/' .. string.upper(project) .. '/repos/' .. repo .. '/browse' .. local_file_path)
end)
