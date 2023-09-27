  document.addEventListener("alpine:init", () => {
    Alpine.data("customerSelect", () => ({
      selected: {
        id: 0,
        phone: "",
        name: "",
      },
      customers: [],
      open: false,

      get openDropdown() {
        return this.open && this.customers.length > 0;
      },
      get selectMask() {
        return this.selected.phone.length > 6 ? "+7(999)999 99-99" : "";
      },
      get isValid() {
          return !this.selected.id &&
            this.selected.name.length > 0 &&
            this.selected.phone.length === 16
            
      },
      resetSelected() {
        this.selected.id = null;
      },
      searchCustomers() {
        let param = new URLSearchParams();
        param.append("phone_ilike", this.selected.phone);

        fetch("/api/customer?" + param.toString()).then((response) =>
          response.json().then((data) => {
            this.customers = data;
          })
        );
      },
    }));
  });