# 🚀 Guide d'utilisation - Auxilium avec IA Colab

## 📋 **Vue d'ensemble**

Votre application Auxilium est maintenant configurée pour utiliser l'IA Colab pour analyser les urgences. Voici comment tout fonctionne :

### 🔄 **Flux complet :**
1. **Utilisateur** → Prend photo + enregistre audio (30s max)
2. **App Mobile** → Envoie vers votre backend FastAPI
3. **Backend** → Transfère vers Colab IA (Qwen2.5-VL)
4. **Colab IA** → Analyse image + audio → Retourne résultat
5. **Backend** → Traite résultat → Notifie utilisateur

---

## 🛠️ **Configuration requise**

### 1. **Serveur Colab démarré** ✅
- Votre code Colab est en cours d'exécution
- Ngrok tunnel actif
- URL publique disponible

### 2. **Backend FastAPI** ✅
- Backend configuré avec Supabase
- Tables créées
- Endpoints IA intégrés

### 3. **App Mobile** ✅
- Interface d'urgence avec photo + audio
- Connexion au backend
- Affichage des résultats IA

---

## 🔧 **Étapes de configuration**

### **Étape 1: Obtenir l'URL Ngrok**
1. Dans votre Colab, copiez l'URL affichée (ex: `https://abc123.ngrok.io`)
2. Ouvrez `backend/config.env`
3. Remplacez `COLAB_AI_URL=https://your-ngrok-url.ngrok.io`
4. Par votre vraie URL : `COLAB_AI_URL=https://abc123.ngrok.io`

### **Étape 2: Tester la connexion**
```bash
cd backend
python test_colab_connection.py
```

### **Étape 3: Démarrer le backend**
```bash
cd backend
python start_api.py
```

### **Étape 4: Démarrer l'app mobile**
```bash
cd frontend_mobile/auxilium_mobile
npx expo start
```

---

## 📱 **Utilisation de l'app**

### **Interface d'urgence :**
1. **Bouton rouge** → "SIGNALER UNE URGENCE"
2. **Photo** → Prendre une photo de la situation
3. **Audio** → Enregistrer un message (max 30s)
4. **Analyse IA** → Bouton "Analyser avec l'IA"
5. **Résultat** → L'IA détermine si c'est une urgence pompiers

### **Résultats possibles :**
- 🚨 **URGENCE DÉTECTÉE** → Pompiers requis
- ✅ **Situation analysée** → Pas d'urgence détectée

---

## 🔍 **Endpoints disponibles**

### **Backend FastAPI :**
- `POST /emergency-sessions` → Créer session + analyse IA
- `GET /emergency-sessions/{id}/ai-result` → Récupérer résultat IA
- `POST /emergency-sessions/{id}/analyze` → Réanalyser
- `GET /ai/status` → Statut connexion IA

### **Colab IA :**
- `GET /` → Santé du serveur
- `POST /analyze` → Analyser urgence

---

## 🧪 **Tests et débogage**

### **Test connexion Colab :**
```bash
cd backend
python test_colab_connection.py
```

### **Test backend :**
```bash
curl http://localhost:8000/ai/status
```

### **Test app mobile :**
1. Ouvrir l'app
2. Aller sur l'écran d'urgence
3. Tester le flux complet

---

## 🚨 **Cas d'usage concrets**

### **Urgence réelle :**
1. Utilisateur voit un feu
2. Prend photo du feu
3. Enregistre : "Il y a un feu dans mon appartement"
4. IA analyse → Détecte feu + fumée
5. Résultat : **URGENCE DÉTECTÉE** → Pompiers requis

### **Fausse alerte :**
1. Utilisateur prend photo normale
2. Enregistre : "Tout va bien"
3. IA analyse → Pas d'urgence
4. Résultat : **Pas d'urgence** → Pas d'action

---

## 🔧 **Dépannage**

### **Problème : "Serveur IA inaccessible"**
- ✅ Vérifiez que Colab est en cours d'exécution
- ✅ Vérifiez l'URL Ngrok dans `config.env`
- ✅ Testez avec `python test_colab_connection.py`

### **Problème : "Network request failed"**
- ✅ Vérifiez que le backend est démarré
- ✅ Vérifiez l'IP dans `emergencyService.ts`
- ✅ Testez avec `curl http://localhost:8000/ai/status`

### **Problème : "Permission refusée"**
- ✅ Vérifiez les permissions caméra/microphone
- ✅ Redémarrez l'app mobile

---

## 📊 **Monitoring**

### **Logs backend :**
- Connexion IA au démarrage
- Analyse des sessions
- Erreurs de connexion

### **Logs Colab :**
- Requêtes reçues
- Temps d'analyse
- Erreurs de traitement

---

## 🎯 **Prochaines étapes**

1. **Implémenter l'upload Supabase** pour les photos/audio
2. **Ajouter la transcription Whisper** pour l'audio
3. **Intégrer les notifications** pour les opérateurs
4. **Ajouter l'historique** des urgences
5. **Optimiser l'interface** utilisateur

---

## 🆘 **Support**

En cas de problème :
1. Vérifiez les logs backend
2. Testez la connexion Colab
3. Vérifiez la configuration
4. Redémarrez les services

**Votre système est maintenant prêt à analyser les urgences avec l'IA !** 🎉
