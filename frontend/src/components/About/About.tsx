import React from 'react';
import './About.css';

const About: React.FC = () => {
  return (
    <div className="about-container">
      <div className="about-hero">
        <div className="hero-content">
          <h1>Sobre o Calendário Solar Israelita</h1>
          <div className="hero-image">
            <img src="/images/sun-cycle.svg" alt="Ciclo Solar" />
          </div>
        </div>
      </div>

      <div className="about-content">
        <section className="mission-section">
          <h2>Nossa Missão</h2>
          <p>O Calendário Solar Israelita é uma ferramenta criada para ajudar as pessoas a compreenderem e acompanharem os ciclos solares conforme descritos nas Escrituras Sagradas. Nossa missão é oferecer um método preciso e acessível para seguir os tempos determinados por YHWH (Deus), com base nos ciclos solares evidenciados na Torá (os cinco primeiros livros da Bíblia), no Livro de Enoque e no Livro dos Jubileus.</p>
        </section>

        <section className="info-section">
          <div className="info-content">
            <h2>O Que é o Calendário Solar?</h2>
            <p>O calendário solar é um sistema de medição do tempo que se baseia no movimento aparente do sol ao longo do ano, marcando eventos importantes como solstícios e equinócios. Diferente dos calendários lunares ou luni-solares, este calendário segue exclusivamente o ciclo solar, refletindo os tempos determinados pelo Criador e alinhando-se com evidências encontradas nas Escrituras Sagradas e descobertas arqueológicas do antigo Israel.</p>
            <p>Além disso, o Calendário Solar Israelita é único por não necessitar de ajustes anuais, permanecendo constante e regular ao longo do tempo. Sua precisão o torna um sistema confiável para calcular os ciclos e marcar eventos de forma inalterável.</p>
          </div>
          <div className="info-image">
            <img src="/images/calendar-cycles.svg" alt="Ciclos do Calendário" />
          </div>
        </section>

        <section className="history-section">
          <h2>História</h2>
          <p>O calendário solar remonta ao período pré-diluviano, sendo mencionado no Livro de Enoque e utilizado para marcar os ciclos das estações, determinados pelo movimento anual do sol. Este sistema foi fundamental na organização das comemorações religiosas e eventos astronômicos, como equinócios e solstícios.</p>
          <p>Além de sua importância religiosa, o calendário solar era uma ferramenta indispensável para prever condições meteorológicas, regular atividades agrícolas e determinar os momentos ideais para plantio e colheita. Civilizações como o Império Romano, o Império Inca e outras adotaram variações desse sistema ao longo dos séculos.</p>
          <p>Embora o calendário gregoriano tenha se tornado o mais amplamente utilizado para fins práticos, é importante lembrar que ele foi significativamente alterado ao longo do tempo. Muitas mudanças, como a redefinição das datas comemorativas e o início do ano, foram feitas para alinhar suas celebrações a cultos pagãos. Ainda assim, sua estrutura reflete os movimentos precisos do sol, sendo um calendário baseado no ciclo solar que não deve ser totalmente desconsiderado.</p>
        </section>

        <section className="reasons-section">
          <h2>Por que um Calendário Solar?</h2>
          <div className="reasons-grid">
            <div className="reason-card">
              <div className="reason-icon">🌟</div>
              <h3>Precisão Astronômica</h3>
              <p>Os ciclos solares são constantes e permitem cálculos exatos.</p>
            </div>
            <div className="reason-card">
              <div className="reason-icon">📖</div>
              <h3>Base Escritural</h3>
              <p>As Escrituras Sagradas, como a Torá e o Livro de Enoque, indicam um calendário baseado no ciclo solar.</p>
            </div>
            <div className="reason-card">
              <div className="reason-icon">⚡</div>
              <h3>Simplicidade e Regularidade</h3>
              <p>O ciclo solar dispensa ajustes anuais complexos, garantindo sua utilização indefinida sem a necessidade de correções.</p>
            </div>
          </div>
        </section>

        <section className="features-section">
          <h2>Recursos do Calendário Solar Israelita</h2>
          <ul className="features-list">
            <li>Cálculos precisos de solstícios e equinócios, ajustados à localização geográfica do usuário.</li>
            <li>Marcação de eventos históricos e celebrações importantes.</li>
            <li>Visualização clara e didática das estações do ano.</li>
            <li>Interface intuitiva e de fácil navegação.</li>
            <li>Informações detalhadas sobre cada evento, alinhadas às tradições israelitas e aos relatos das Escrituras Sagradas.</li>
          </ul>
        </section>

        <section className="development-section">
          <h2>Desenvolvimento</h2>
          <p>Este calendário foi criado por Sanyahu Ben Shem, seguidor da fé israelita, pesquisador das Escrituras Sagradas e webdesigner brasileiro. Após anos de estudo dedicado ao Calendário Solar mencionado na Torá, no Livro de Enoque e no Livro dos Jubileus, Sanyahu desenvolveu esta ferramenta com o objetivo de torná-la precisa, acessível e fiel aos princípios estabelecidos por YHWH (Deus).</p>
          <p>Com o uso de tecnologias modernas, o calendário foi projetado para garantir exatidão nos cálculos astronômicos e oferecer aos usuários uma experiência prática e significativa, conectando as tradições israelitas ao ciclo solar.</p>
        </section>

        <section className="objective-section">
          <h2>Nosso Objetivo</h2>
          <p>O objetivo principal deste calendário é permitir a observância das comemorações perpétuas descritas na Torá (Levítico 23), entregues por YHWH (Deus) a Moisés. Este trabalho busca garantir que essas celebrações ocorram nos dias designados, preservando a tradição e a fidelidade às Escrituras Sagradas.</p>
        </section>

        <section className="contribute-section">
          <div className="contribute-content">
            <h2>Contribua</h2>
            <p>Valorizamos seu feedback! Caso tenha sugestões ou identifique algo que possa ser aprimorado, entre em contato conosco através do botão de contato no rodapé da página.</p>
          </div>
          <div className="contribute-image">
            <img src="/images/feedback.svg" alt="Feedback" />
          </div>
        </section>
      </div>
    </div>
  );
};

export default About;
