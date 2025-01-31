local telescope_setup, telescope = pcall(require, "telescope")
if not telescope_setup then
	return
end

local actions_setup, actions = pcall(require, "telescope.actions")
if not actions_setup then
	return
end

telescope.setup({
    defaults = {
        mappings = {
			-- i = {
			-- 	["<C-k>"] = actions.move_selection_previous, -- move to prev result
			-- 	["<C-j>"] = actions.move_selection_next, -- move to next result
			-- 	["<C-q>"] = actions.send_selected_to_qflist + actions.open_qflist, -- send selected to quickfixlist
			-- },
		},
	},
})

telescope.load_extension("fzf")


local builtin = require('telescope.builtin')
local keymap = vim.keymap
vim.keymap.set('n', '<leader>t', builtin.find_files, {})
vim.keymap.set('n', '<leader>s', builtin.live_grep, {})
vim.keymap.set('n', '<leader>b', builtin.buffers, {})
-- vim.keymap.set('n', '<leader>fh', builtin.help_tags, {})
