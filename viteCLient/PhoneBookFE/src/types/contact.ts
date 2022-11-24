interface Contact {
    id?: string;
    name?: string;
    phone?: string;
    email?: string;
    address?: Address;
    company?: string;
    notes?: string;
};

interface Address {
    street?: string;
    city?: string;
    state?: string;
    zipcode?: string;
    country?: string;
};



export type { Contact, Address };