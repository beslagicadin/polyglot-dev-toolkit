const { DOMUtils, APIClient, DataUtils, ValidationUtils, StorageUtils } = require('../../src/javascript/utils');

// Test suite for DOMUtils
describe('DOMUtils', () => {
    test('creates element with specified attributes and content', () => {
        const element = DOMUtils.createElement('div', { className: 'test', style: { color: 'red' } }, 'Hello World');
        expect(element.tagName).toBe('DIV');
        expect(element.className).toBe('test');
        expect(element.style.color).toBe('red');
        expect(element.innerHTML).toBe('Hello World');
    });

    test('waitForElement function finds existing element', async () => {
        document.body.innerHTML = '<div id="test"></div>';
        const element = await DOMUtils.waitForElement('#test', 1000);
        expect(element.id).toBe('test');
    });
});

// Test suite for APIClient
describe('APIClient', () => {
    test('performs GET request', async () => {
        const client = new APIClient('/api');
        window.fetch = jest.fn().mockResolvedValue({
            ok: true,
            json: async () => ({ data: 'test' }),
            headers: { get: () => 'application/json' },
        });
        const response = await client.get('/data');
        expect(response.data).toBe('test');
    });
});

// Test suite for ValidationUtils
describe('ValidationUtils', () => {
    test('validates email address', () => {
        expect(ValidationUtils.isValidEmail('test@example.com')).toBe(true);
        expect(ValidationUtils.isValidEmail('invalid-email')).toBe(false);
    });

    test('validates URL', () => {
        expect(ValidationUtils.isValidURL('https://example.com')).toBe(true);
        expect(ValidationUtils.isValidURL('invalid-url')).toBe(false);
    });
});

// Test suite for DataUtils
describe('DataUtils', () => {
    test('deep clones objects', () => {
        const obj = { a: 1, b: { c: 2 } };
        const clone = DataUtils.deepClone(obj);
        expect(clone).toEqual(obj);
        expect(clone).not.toBe(obj);
    });

    test('removes duplicates from array', () => {
        const array = [{ id: 1 }, { id: 2 }, { id: 1 }];
        const result = DataUtils.removeDuplicates(array, 'id');
        expect(result).toHaveLength(2);
    });
});
