print("Events in the Network:")
print("1.Burglary(B)")
print("2.Earthquake(E)")
print("3.Alarm(A)")
print("4.John Calls(J)")
print("5.Mary Calls(M)")

print("\nEnter Probabilities")
P_B = float(input("Enter P(B):"))
P_E = float(input("Enter P(E):"))
P_J_A = float(input("Enter P(J|A):"))
P_J_notA = float(input("Enter P(J|~A):"))
P_M_A = float(input("Enter P(M|A):"))
P_M_notA = float(input("Enter P(M|~A):"))

print("\nEnter Alarm Probabilities")
P_A_BT_ET = float(input("Enter P(A|B=1,E=1):"))
P_A_BT_EF = float(input("Enter P(A|B=1,E=0):"))
P_A_BF_ET = float(input("Enter P(A|B=0,E=1):"))
P_A_BF_EF = float(input("Enter P(A|B=0,E=0):"))

while True:
    print("\n1.Enter Query")
    print("2.Exit")
    ch = int(input("Enter your choice:"))

    if ch == 1:
        print("\nEnter values(1=True,0=False)")
        B = int(input("Enter B:"))
        E = int(input("Enter E:"))
        A = int(input("Enter A:"))
        J = int(input("Enter J:"))
        M = int(input("Enter M:"))

        p = 1

        if B == 1: p = p * P_B
        else:      p = p * (1 - P_B)

        if E == 1: p = p * P_E
        else:      p = p * (1 - P_E)

        if   B == 1 and E == 1: pa = P_A_BT_ET
        elif B == 1 and E == 0: pa = P_A_BT_EF
        elif B == 0 and E == 1: pa = P_A_BF_ET
        else:                   pa = P_A_BF_EF

        if A == 1: p = p * pa
        else:      p = p * (1 - pa)

        if J == 1:
            if A == 1: p = p * P_J_A
            else:      p = p * P_J_notA
        else:
            if A == 1: p = p * (1 - P_J_A)
            else:      p = p * (1 - P_J_notA)

        if M == 1:
            if A == 1: p = p * P_M_A
            else:      p = p * P_M_notA
        else:
            if A == 1: p = p * (1 - P_M_A)
            else:      p = p * (1 - P_M_notA)

        print("Joint Probability =", format(p, '.9f'))

    elif ch == 2:
        break
    else:
        print("Invalid choice")