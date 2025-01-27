-- To-do: Rename setup to status?
local setup, lualine = pcall(require, 'lualine')
if not setup then
  return
end

local lualine_nightfly = require('lualine.themes.nightfly')

-- To-do: Better colors?

lualine.setup({
  options = {
    theme = lualine_nightfly,
    icons_enabled = false,
  },
})
