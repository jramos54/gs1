:::mermaid
erDiagram
    ATRIBUTOS ||--o{ PRODUCTOS : tiene
    ATRIBUTOS {
        int id_atributo PK
        string nombre_atributo
    }
    PRODUCTOS {
        string GTIN PK
        int id_atributo FK
        string valor_atributo
    }
