from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor

class ScoreEstimator:
    ...
    def predict(self, student_name: str, target_assessment: str, model_type: str = "linear") -> dict:
        if self.df is None:
            raise ValueError("No data loaded")

        if student_name not in set(self.get_students()):
            raise ValueError(f"Unknown student: {student_name}")
        if target_assessment not in set(self.get_assessments()):
            raise ValueError(f"Unknown assessment: {target_assessment}")

        X, y, features = self._training_frame(target_assessment)

        # Select model
        if model_type == "ridge":
            model = Ridge(alpha=1.0)
        elif model_type == "decision_tree":
            model = DecisionTreeRegressor(max_depth=5, random_state=42)
        else:
            model = LinearRegression()

        model.fit(X, y)

        # Student feature vector
        train_means = X.mean(numeric_only=True)
        student_row = self.df[self.df["Student"].astype(str) == str(student_name)][features].copy()
        student_row = student_row.apply(pd.to_numeric, errors="coerce").fillna(train_means)

        predicted = float(model.predict(student_row)[0])
        predicted = max(0.0, min(100.0, predicted))  # clamp to 0–100

        # Save prediction
        self.predictions.setdefault(student_name, {})[target_assessment] = predicted

        # Stats
        student_avg = float(
            self.df.loc[self.df["Student"].astype(str) == str(student_name), features]
            .apply(pd.to_numeric, errors="coerce")
            .mean(axis=1)
            .fillna(0)
            .values[0]
        )
        class_avg = float(y.mean())
        confidence = float(max(0.0, min(1.0, model.score(X, y))))

        return {
            "student": student_name,
            "assessment": target_assessment,
            "modelUsed": model_type,
            "predictedScore": round(predicted, 1),
            "classAverage": round(class_avg, 1),
            "studentAverage": round(student_avg, 1),
            "confidence": round(confidence, 2),
            "trainingSamples": int(len(X))
        }
