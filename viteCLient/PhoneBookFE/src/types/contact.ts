interface Contact {
    id?: number;
    name?: string;
    phone?: string;
    email?: string;
    address?: Address;
    company?: Company;
    notes?: string;
}

interface Address {
    street?: string;
    city?: string;
    state?: string;
    zipcode?: string | number;
}

interface Company {
    name?: string;
    address?: Address;
}

export type { Contact, Address };