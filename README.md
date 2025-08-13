# 📦 API Usuários

Um CRUD simples desenvolvido com **Spring Boot** e **React JS**, ideal para quem está começando com aplicações full stack e deseja entender a integração entre front-end e back-end.

## 🚀 Tecnologias Utilizadas

### Back-end
- **Java** com **Spring Boot**
- **Spring Data JPA**
- **H2 Database** (ou outro banco relacional)
- **Maven**

### Front-end
- **React JS**
- **Axios** para requisições HTTP
- **CSS/HTML** para estilização básica

## 📁 Estrutura do Projeto

```
api-usuarios/
├── back-end/
│   └── src/
│       └── main/
│           └── java/
│               └── com.example.apiusuarios/
│                   ├── controller/
│                   ├── model/
│                   ├── repository/
│                   └── service/
├── front-end/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── App.js
```

## ⚙️ Funcionalidades

- Criar usuários
- Listar todos os usuários
- Atualizar dados de um usuário
- Excluir usuários
- Upload de arquivos (corrigido recentemente)

## 📦 Como Executar

### Back-end
```bash
cd back-end
./mvnw spring-boot:run
```

### Front-end
```bash
cd front-end
npm install
npm start
```

## 🧪 Testes

Você pode testar a API usando o Postman ou diretamente pelo front-end React.

## 📌 Observações

Este projeto é uma base simples e pode ser expandido com autenticação, validações, paginação e muito mais.

