// vitest.config.ts
import { defineConfig } from 'vitest/config'
import {resolve} from "pathe";

export default defineConfig({
    test: {
        globals: true,
        environment: 'jsdom',
        setupFiles: './setupTests.ts',
    },
    resolve: {
        alias: {
            '@': resolve(__dirname, './'),
        },
    },
})