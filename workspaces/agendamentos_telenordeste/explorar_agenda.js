// Script para extrair informações da página de agendamento

const analise = {
  url: window.location.href,
  titulo: document.title,
  
  // Elementos de formulário
  inputs: Array.from(document.querySelectorAll('input')).map(input => ({
    tipo: input.type,
    nome: input.name,
    id: input.id,
    placeholder: input.placeholder,
    required: input.required,
    value: input.value
  })),
  
  // Selects (dropdowns)
  selects: Array.from(document.querySelectorAll('select')).map(select => ({
    nome: select.name,
    id: select.id,
    opcoes: Array.from(select.options).map(opt => opt.text)
  })),
  
  // Botões
  botoes: Array.from(document.querySelectorAll('button, input[type="button"], input[type="submit"]')).map(btn => ({
    texto: btn.textContent || btn.value,
    tipo: btn.type,
    id: btn.id,
    classes: btn.className
  })),
  
  // Links
  links: Array.from(document.querySelectorAll('a')).slice(0, 20).map(link => ({
    texto: link.textContent.trim(),
    href: link.href
  })),
  
  // Tabelas
  tabelas: Array.from(document.querySelectorAll('table')).length,
  
  // Divs que podem ser calendário ou cards
  divsComClasse: Array.from(document.querySelectorAll('div[class*="calendar"], div[class*="date"], div[class*="agenda"], div[class*="schedule"]')).map(div => ({
    classes: div.className,
    id: div.id
  })),
  
  // Scripts externos
  scripts: Array.from(document.querySelectorAll('script[src]')).map(script => script.src),
  
  // Textos visíveis principais
  headings: Array.from(document.querySelectorAll('h1, h2, h3, h4')).map(h => ({
    tag: h.tagName,
    texto: h.textContent.trim()
  }))
};

console.log(JSON.stringify(analise, null, 2));
