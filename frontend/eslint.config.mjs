// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'
import prettierConfig from 'eslint-config-prettier'; // <-- ADD THIS IMPORT

export default withNuxt(
  // 1. Your custom rules object
  {
    rules: {
      // You can override or add any rules you want here.
      // For example:
      'vue/multi-word-component-names': 'off',
      'semi': ['error', 'always'],
    }
  },

  // 2. The Prettier config.
  // This MUST be the last item in the array to properly
  // disable any conflicting rules from the base Nuxt config.
  prettierConfig
)
