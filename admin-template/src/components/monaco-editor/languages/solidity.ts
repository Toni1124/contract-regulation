export function registerSolidityLanguage(monaco: any) {
  monaco.languages.register({ id: 'solidity' })

  monaco.languages.setMonarchTokensProvider('solidity', {
    keywords: [
      'contract', 'library', 'interface', 'function', 'modifier',
      'event', 'struct', 'enum', 'mapping', 'address', 'bool',
      'string', 'bytes', 'uint', 'int', 'fixed', 'ufixed',
      'public', 'private', 'external', 'internal', 'payable',
      'view', 'pure', 'constant', 'storage', 'memory', 'calldata',
      'returns', 'return', 'if', 'else', 'for', 'while', 'do',
      'break', 'continue', 'throw', 'import', 'using', 'pragma',
      'solidity', 'assembly', 'this', 'super', 'new', 'delete',
      'require', 'assert', 'revert'
    ],

    operators: [
      '=', '>', '<', '!', '~', '?', ':',
      '==', '<=', '>=', '!=', '&&', '||', '++', '--',
      '+', '-', '*', '/', '&', '|', '^', '%', '<<',
      '>>', '>>>', '+=', '-=', '*=', '/=', '&=', '|=',
      '^=', '%=', '<<=', '>>=', '>>>='
    ],

    symbols: /[=><!~?:&|+\-*\/\^%]+/,

    tokenizer: {
      root: [
        [/[a-zA-Z_]\w*/, { 
          cases: {
            '@keywords': 'keyword',
            '@default': 'identifier'
          }
        }],
        [/[{}()\[\]]/, '@brackets'],
        [/@symbols/, { 
          cases: {
            '@operators': 'operator',
            '@default': ''
          }
        }],
        [/\d*\.\d+([eE][\-+]?\d+)?/, 'number.float'],
        [/\d+/, 'number'],
        [/\".*?\"/, 'string'],
        [/\/\/.*$/, 'comment'],
        [/\/\*/, 'comment', '@comment'],
      ],
      comment: [
        [/[^\/*]+/, 'comment'],
        [/\*\//, 'comment', '@pop'],
        [/[\/*]/, 'comment']
      ]
    }
  })
} 