Os custos de geração de 1 MWatt pela termoelétrica $\text{CT}$ e da variação de $1m^3$ no reservatório $\text{CA}$ são constantes dadas.

- O reservatório começa com um volume inicial de água 
$\text{V}_{\text{ini}}$  
e tem limites mínimo e máximo (constantes dadas) para o volume de água $m^3$ e que devem ser respeitados, respectivamente 
$\text{V}_{\text{min}}$ e $\text{V}_{\text{max}}$.

- A cada mês, o reservatoório recebe um volume de água $m_3$ proveniente de chuvas, afluências, etc. Essas informações foram estimadas para os $n$ mesesdo planejamento e são constatnes dadas, $y_1, y_2, ..., y_n$.

- A única forma do volume de água no reservatório diminuir é turbinando a água para gerar energia. A cada $1m^3$ de água turbinada, gera-se 
$kMWatt$ de energia, onde $k$ é uma constante dada.

- Há uma capacidade máxima de geração mensal da termoelétrica, que é uma constante $t_{max}$.

- As demandas mensais da cidade (MWatt) também são constantes $d_1, d_2, . . . , d_n$
dadas e devem ser atendidas pela geração de energia da hidrelétrica e
da termoelétrica. Gerar mais do que a demanda não é um problema (a
energia restante vai para outra cidade, por exemplo).

sendo as variáveis:
- $V_i =$ Volume da hidrelétrica no mês $i$
- $T_i =$ Volume Turbinado no mês $i$
- $G_i =$ Energia gerada pela Termoelétrica no mês $i$

$$\large
\begin{equation}
\begin{align*}
\begin{split}
& min:  \text{CA}\sum_{i = 1}^{n}{|y_i - T_i|} + 
        \text{CT}\sum_{j = 1}^{n}{G_j} \\
& s.a.:\\
& d_i \le kT_i + G_i \\
& V_i = V_{i-1} + y_i - T_i \\ 
\\
& V_1 =  V_{ini} + y_1 - T_1 \\
& V_{min} \le V_i \le V_{max} \\
& T_i, G_i \ge 0 \\
& i \in \mathbb{Z}, [1, 2, ..., n]
\end{split}
\end{align*}
\end{equation}
$$

Mas como a operação de módulo deve ser removida, seguimos o truque
$$\Large
\begin{equation}
\begin{split}
& x_i - x_{i-1} = A_i - B_i \\
& |x_i - x_{i-1}| = A_i + B_i \\
& s.a.: A_i, B_i \ge 0
\end{split}
\end{equation}
$$

De forma a representar $A_i$ como o incremento no volume e $B_i$ o decremento.

<!-- Como $V_i = V_{i-1} + y_i + T_i$, temos então que -->
$$\large
\begin{equation}
\begin{split}
& |y_i - T_i| = A_i + B_i \\
& y_i - T_i = A_i - B_i \\
& \implies \\
& A_i = y_i - T_i + B_i
\end{split}
\end{equation}
$$ 
Portanto, ao nos livrarmos do módulo com $A_i + B_i$ , respeitando $(2)$ e reformulando o problema como $(3)$ temos então 

---
$$\large
\begin{equation}
\begin{align*}
\begin{split}
& min:  \text{CA}\sum_{i = 1}^{n}{(A_i + B_i)} + 
        \text{CT}\sum_{j = 1}^{n}{G_j} \\
& s.a.:\\
& d_i \le kT_i + G_i \\
& V_i = V_{i-1} + y_i - T_i \\ 
& A_i = y_i - T_i + B_i \\
\\
& V_1 =  V_{ini} + y_1 - T_1 \\
& V_{min} \le V_i \le V_{max} \\
& A_i, B_i,G_i,T_i \ge 0 \\
& i \in \mathbb{Z}, [1, 2, ..., n]
\end{split}
\end{align*}
\end{equation}
$$

E com isso chegamos ao resultado ótimo esperado com $(4)$.