# 30-day trial

## Release availability

Trial enforcement is being prepared for a future release. The currently published `0.1.0-beta.1` image has no trial expiry. No trial-enabled image has been published yet. Use this guide once Cloud-Visi supplies the new release image.

## Activate your installation

1. Install the trial-enabled release using the normal Kubernetes or optional Compose guide.
2. Open the application. The activation page shows your **Installation ID**.
3. Share that ID with your Cloud-Visi contact. It is not a code-host credential.
4. Paste the trial key they supply and select **Activate trial**.

The key is bound to that installation and has a fixed expiry, no more than 30 days after its start. The countdown starts when the key is issued, not when it is pasted into the app. The app checks the signed key locally. Activation does not send your repositories or credentials to a licensing service.

Settings > General shows your expiry date and lets you enter a replacement key. A reminder appears during the final seven days. Changing the server clock backwards can suspend access; correct the clock and check status again.

## When the trial ends

New syncs stop, and normal application access is paused. The activation page remains available so you can enter a new key. Health and database readiness checks continue to work; an expired trial should not make Kubernetes restart the pod repeatedly.

Your database, cloned repositories, history, and saved settings remain stored. Expiry does not delete them. Keep the database and repository volumes, and keep the same encryption key. Your platform team can continue to back up the database using the [operations guide](operations.md).

Reinstalling against the same database or restarting the container does not restart the trial. Restoring that database also restores its Installation ID and saved trial key. A new empty database has a different ID and needs a separately issued key. A key for another installation will be refused.

## Optional Kubernetes key mount

UI activation is sufficient. If your platform team wants to provision the key as a file instead, create a dedicated Secret from the supplied file and reference it in the chart. Do not put keys in a committed values file.

```bash
CONTEXT=your-context-name
kubectl --context "$CONTEXT" -n cloud-visi create secret generic cloud-visi-trial \
  --from-file=trial-key=/absolute/path/to/trial-key.txt
helm upgrade cloud-visi ./charts/cloud-visi \
  --kube-context "$CONTEXT" --namespace cloud-visi \
  --reuse-values --set trial.existingSecret=cloud-visi-trial
```

These commands assume an existing installation is already using the supplied trial-enabled image. The chart mounts the Secret read-only. The application imports it on startup. After replacing a mounted key, restart the application pod so it imports the new file. UI activation takes effect without a restart.

An unreadable, invalid, or expired mounted file does not overwrite a valid key already saved in the database. Keep using the same database and existing deployment Secret when upgrading.

## Optional Docker Compose key mount

UI activation also works with Compose. For a file mount, use the overlay:

```bash
TRIAL_LICENSE_PATH=/absolute/path/to/trial-key.txt \
  docker compose -f compose.yaml -f compose.trial.yaml up -d --wait --wait-timeout 600
```

Keep the supplied trial image selection in your existing `.env`, along with the database password and encryption key. Make the trial file readable by the application's UID 10001. The overlay refuses a missing source file instead of creating a directory in its place. Use the same overlay for later restarts. Never run `down -v` to renew a trial; that deletes your data.

## Limits

This is offline application enforcement, not a tamper-proof licensing service. Someone who controls the host, binary, database backups, or an older unrestricted image can bypass local restrictions. The technical trial mechanism does not choose or replace the written evaluation licence, which remains undecided.
