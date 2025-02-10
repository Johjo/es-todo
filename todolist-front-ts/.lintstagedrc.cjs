module.exports = {
  '*.{css,scss}': ['stylelint --fix --allow-empty-input', 'prettier --write'],
  '*.pug': 'prettier --write',
  '{src/**/,}*.{ts,tsx}': ['eslint --fix', 'prettier --write'],
  '*.{md,json*,yml,html,css,scss,java,xml,feature}': ['prettier --write'],
};
