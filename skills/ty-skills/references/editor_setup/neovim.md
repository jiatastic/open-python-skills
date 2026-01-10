# Neovim Setup for ty

Configure ty as your Python type checker and language server in Neovim.

## Installation

### 1. Install ty

```bash
# Using uv (recommended)
uv tool install ty

# Or with pip
pip install ty

# Verify
ty --version
```

### 2. Configure Neovim

ty provides a language server. Configure it with your preferred LSP client.

## nvim-lspconfig Setup

### Basic Configuration

```lua
-- lua/plugins/ty.lua or init.lua

local lspconfig = require('lspconfig')

-- Register ty as a language server
local configs = require('lspconfig.configs')

if not configs.ty then
  configs.ty = {
    default_config = {
      cmd = { 'ty', 'server' },
      filetypes = { 'python' },
      root_dir = lspconfig.util.root_pattern(
        'pyproject.toml',
        'ty.toml',
        '.git'
      ),
      settings = {},
    },
  }
end

-- Enable ty
lspconfig.ty.setup({
  on_attach = function(client, bufnr)
    -- Key mappings
    local opts = { buffer = bufnr }
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
    vim.keymap.set('n', 'gr', vim.lsp.buf.references, opts)
    vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, opts)
    vim.keymap.set('n', '<leader>ca', vim.lsp.buf.code_action, opts)
  end,
})
```

### With mason.nvim

```lua
-- lua/plugins/mason.lua

return {
  {
    'williamboman/mason.nvim',
    config = true,
  },
  {
    'williamboman/mason-lspconfig.nvim',
    dependencies = { 'mason.nvim' },
    config = function()
      require('mason-lspconfig').setup({
        ensure_installed = { 'ty' },  -- When available in mason
      })
    end,
  },
  {
    'neovim/nvim-lspconfig',
    dependencies = { 'mason-lspconfig.nvim' },
    config = function()
      local lspconfig = require('lspconfig')
      
      lspconfig.ty.setup({
        -- Configuration here
      })
    end,
  },
}
```

## LazyVim Configuration

If using LazyVim:

```lua
-- lua/plugins/ty.lua

return {
  {
    'neovim/nvim-lspconfig',
    opts = {
      servers = {
        ty = {
          cmd = { 'ty', 'server' },
          filetypes = { 'python' },
        },
      },
    },
  },
}
```

## Disable Conflicting Servers

To avoid conflicts with pyright or pylsp:

```lua
-- Disable other Python LSPs when using ty
lspconfig.pyright.setup({
  autostart = false,  -- Don't auto-start pyright
})

-- Or use a condition
local python_lsp = vim.fn.executable('ty') == 1 and 'ty' or 'pyright'

if python_lsp == 'ty' then
  lspconfig.ty.setup({})
else
  lspconfig.pyright.setup({})
end
```

## Key Mappings

Recommended keybindings for ty:

```lua
-- After ty is attached
local on_attach = function(client, bufnr)
  local opts = { buffer = bufnr, noremap = true, silent = true }
  
  -- Navigation
  vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
  vim.keymap.set('n', 'gD', vim.lsp.buf.declaration, opts)
  vim.keymap.set('n', 'gi', vim.lsp.buf.implementation, opts)
  vim.keymap.set('n', 'gr', vim.lsp.buf.references, opts)
  vim.keymap.set('n', 'gt', vim.lsp.buf.type_definition, opts)
  
  -- Information
  vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
  vim.keymap.set('n', '<C-k>', vim.lsp.buf.signature_help, opts)
  
  -- Refactoring
  vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, opts)
  vim.keymap.set('n', '<leader>ca', vim.lsp.buf.code_action, opts)
  
  -- Diagnostics
  vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, opts)
  vim.keymap.set('n', ']d', vim.diagnostic.goto_next, opts)
  vim.keymap.set('n', '<leader>e', vim.diagnostic.open_float, opts)
  vim.keymap.set('n', '<leader>q', vim.diagnostic.setloclist, opts)
end
```

## Diagnostics Display

Configure diagnostic appearance:

```lua
vim.diagnostic.config({
  virtual_text = {
    prefix = '●',
    source = 'if_many',
  },
  float = {
    border = 'rounded',
    source = 'always',
  },
  signs = true,
  underline = true,
  update_in_insert = false,
  severity_sort = true,
})

-- Custom diagnostic signs
local signs = { Error = '', Warn = '', Hint = '', Info = '' }
for type, icon in pairs(signs) do
  local hl = 'DiagnosticSign' .. type
  vim.fn.sign_define(hl, { text = icon, texthl = hl, numhl = hl })
end
```

## Integration with null-ls / none-ls

If you want ty as a diagnostic source:

```lua
local null_ls = require('null-ls')

null_ls.setup({
  sources = {
    null_ls.builtins.diagnostics.ty.with({
      extra_args = { '--output-format', 'json' },
    }),
  },
})
```

## Telescope Integration

Find references and definitions with Telescope:

```lua
vim.keymap.set('n', 'gr', function()
  require('telescope.builtin').lsp_references()
end, { desc = 'Find references' })

vim.keymap.set('n', 'gd', function()
  require('telescope.builtin').lsp_definitions()
end, { desc = 'Go to definition' })

vim.keymap.set('n', '<leader>ds', function()
  require('telescope.builtin').lsp_document_symbols()
end, { desc = 'Document symbols' })
```

## Troubleshooting

### ty server not starting

Check if ty is in PATH:

```bash
which ty
ty server --help
```

Check Neovim logs:

```vim
:LspLog
```

### Slow Startup

ty is fast, but for large projects:

```toml
# pyproject.toml
[tool.ty.src]
exclude = [
  "**/node_modules",
  "**/.venv",
  "**/build"
]
```

### No Diagnostics

Ensure:

1. ty is running: `:LspInfo`
2. File type is Python: `:set ft?`
3. Project has `pyproject.toml` or `ty.toml`

### Conflicts with Other LSPs

Only one Python LSP should be active:

```lua
-- Check active clients
:lua print(vim.inspect(vim.lsp.get_active_clients()))

-- Manually stop a client
:lua vim.lsp.stop_client(client_id)
```
